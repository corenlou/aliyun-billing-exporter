import json
import os
import datetime
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
from aliyunsdkcore.client import AcsClient
from aliyunsdkbssopenapi.request.v20171214.QueryInstanceBillRequest import QueryInstanceBillRequest

app = Flask(__name__)

# -----------------------
# 配置说明：
# 多账号：用 ; 分隔
# 多月份：自动从 START_MONTH 统计到当前月（含）
# -----------------------

ACCESS_KEYS = os.getenv("ALIYUN_ACCESS_KEY").split(";")
SECRET_KEYS = os.getenv("ALIYUN_SECRET_KEY").split(";")
REGIONS = os.getenv("ALIYUN_REGION", "cn-hangzhou").split(";")
ACCOUNT_NAME = os.getenv("ACCOUNT").split(";")
START_MONTH = os.getenv("START_MONTH")  # 例如 2024-08


def month_range(start):
    """生成从 start 到当前月的月份列表"""
    start_date = datetime.datetime.strptime(start, "%Y-%m")
    now = datetime.datetime.now()

    months = []
    cur = start_date

    while cur <= now:
        months.append(cur.strftime("%Y-%m"))
        year = cur.year + (cur.month // 12)
        month = cur.month % 12 + 1
        cur = datetime.datetime(year, month, 1)

    return months


def fetch_all_bills_for_month(client, month):
    bills = []
    page = 1
    page_size = 100

    while True:
        request = QueryInstanceBillRequest()
        request.set_accept_format("json")
        request.set_BillingCycle(month)
        request.set_PageSize(page_size)
        request.set_PageNum(page)

        response = json.loads(client.do_action_with_exception(request))
        data = response["Data"]

        bills.extend(data.get("Items", {}).get("Item", []))

        if page * page_size >= data["TotalCount"]:
            break
        page += 1

    return bills


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()

    g_total = Gauge(
        "aliyun_bill_total_cost",
        "Total bill amount for month",
        ["account", "month"],
        registry=registry
    )

    g_product = Gauge(
        "aliyun_bill_product_cost",
        "Cost by product for each month",
        ["account", "month", "product"],
        registry=registry
    )

    g_product_type = Gauge(
        "aliyun_bill_product_billing_type_cost",
        "Cost by product and billing type for each month",
        ["account", "month", "product", "type"],
        registry=registry
    )

    months = month_range(START_MONTH)

    # 多账号循环
    #names = ["ltex", "biking"]
    for idx, (ak, sk) in enumerate(zip(ACCESS_KEYS, SECRET_KEYS)):
        region = REGIONS[idx] if idx < len(REGIONS) else REGIONS[0]
        #account_name = f"account{idx+1}"
        account_name = ACCOUNT_NAME[idx]

        client = AcsClient(ak, sk, region)

        for month in months:
            bills = fetch_all_bills_for_month(client, month)

            total_cost = 0.0
            product_sum = {}
            product_type_sum = {}

            for item in bills:
                product = item.get("ProductCode", "Unknown")
                amount = float(item.get("PretaxAmount", 0))

                # 判断是否预付费（简单逻辑）
                #billing_type = "Prepaid" if item.get("Item", "").startswith("Prepaid") else "Postpaid"
                billing_type = (
                    "Prepaid" if item.get("Item", "").startswith("Subscription")
                    else "Postpaid" if item.get("Item", "").startswith("PayAsYouGo")
                    #else "Refund" if item.get("Item", "").startswith("Refund")
                    else "Others"
                )

                total_cost += amount

                product_sum[product] = product_sum.get(product, 0) + amount
                product_type_sum[(product, billing_type)] = product_type_sum.get((product, billing_type), 0) + amount

            # 写入 metrics
            g_total.labels(account=account_name, month=month).set(total_cost)

            for product, amount in product_sum.items():
                g_product.labels(account=account_name, month=month, product=product).set(amount)

            for (product, billing_type), amount in product_type_sum.items():
                g_product_type.labels(
                    account=account_name,
                    month=month,
                    product=product,
                    type=billing_type
                ).set(amount)

    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)


@app.route("/")
def index():
    return "Aliyun Billing Exporter (multi-account, multi-month). Visit /metrics"


if __name__ == "__main__":
    port = int(os.getenv("EXPORTER_PORT", "9105"))
    app.run(host="0.0.0.0", port=port)

