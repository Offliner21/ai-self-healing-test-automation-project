from zapv2 import ZAPv2
import time
import os

# Configuration
ZAP_PROXY = "http://127.0.0.1:8080"
# Ensure the port and protocol match your running app exactly
TARGET = "http://host.docker.internal:3000/"

zap = ZAPv2(
    proxies={
        'http': ZAP_PROXY,
        'https': ZAP_PROXY
    }
)


def wait_for_zap():
    print(f"[ZAP] Connecting to ZAP at {ZAP_PROXY}...")
    for _ in range(15):
        try:
            zap.core.version
            print("[ZAP] Connected successfully!")
            return
        except Exception:
            print("[ZAP] Waiting for ZAP to initialize...")
            time.sleep(3)
    raise Exception("Error: ZAP not reachable. Check if Docker container is running.")


def run_zap_scan():
    wait_for_zap()

    print(f"[ZAP] Accessing target to seed ZAP: {TARGET}")
    zap.core.access_url(TARGET)
    time.sleep(2)

    # 1. Start Spider
    print(f"[ZAP] Starting Spider...")
    spider_id = zap.spider.scan(TARGET)

    # Validation: Ensure spider_id is actually an ID
    if not str(spider_id).isdigit():
        print(f"[ERROR] Spider failed to start. ZAP returned: {spider_id}")
        return

    while int(zap.spider.status(spider_id)) < 100:
        print(f"[ZAP] Spider progress: {zap.spider.status(spider_id)}%")
        time.sleep(2)
    print("[ZAP] Spider complete.")

    # 2. Verify Site Tree
    # If the spider found 0 URLs, Active Scan WILL fail
    if not zap.core.hosts:
        print("[ERROR] Spider found 0 pages. Active Scan aborted.")
        print("Check if your app is running and reachable at host.docker.internal:3000")
        return

    # 3. Active Scan
    print(f"[ZAP] Starting Active Scan...")
    ascan_id = zap.ascan.scan(TARGET)

    if not str(ascan_id).isdigit():
        print(f"[ERROR] Active Scan failed to start. ZAP returned: {ascan_id}")
        return

    while int(zap.ascan.status(ascan_id)) < 100:
        print(f"[ZAP] Active Scan progress: {zap.ascan.status(ascan_id)}%")
        time.sleep(5)
    print("[ZAP] Active Scan complete.")

    # 4. Generate Report
    if not os.path.exists("reports"):
        os.makedirs("reports")

    print("[ZAP] Saving report...")
    with open("reports/zap_report.html", "w", encoding="utf-8") as f:
        f.write(zap.core.htmlreport())
    print(f"[ZAP] Success! Report saved to reports/zap_report.html")


if __name__ == "__main__":
    run_zap_scan()
