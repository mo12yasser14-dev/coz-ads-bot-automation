import requests
import json
from datetime import datetime
import time

# بيانات Meta
BUSINESS_ACCOUNT_ID = "369769028309919"
AD_ACCOUNT_ID = "1724022672286258"
ACCESS_TOKEN = "EAAUdgtxsZBFEBSHnjkACm0iESzN4ZCjZAftZBREfoZA3f2ahQqLTVe2eIpQqsMbUL5BlwGukQ9eFFg8KBuSNbs25GS1OZCZBtw71cWTydvNybPKoBbZA5hjIlqW38YAH5cprz69TMH9iOQbIAibDnWDMbZCIVYoNLbue3LqeZAgyhdN6b9EuzMM9UHeXTGpcruYJsXhZCMwWPW48ZAwBw78A9gjjCq7cNhmBQFblZBZBeddpAFxSPIMeI56phg9Ci7Xr0IQZADoe0tWKw82MO38XMYD4Ltb"

BASE_URL = "https://graph.instagram.com/v18.0"
META_API_URL = "https://graph.facebook.com/v18.0"

class COZAAdManager:
    def __init__(self, ad_account_id, access_token):
        self.ad_account_id = ad_account_id
        self.access_token = access_token
        self.min_roi = 2.0
        self.max_roi = 5.0
        
    def get_campaigns(self):
        url = f"{META_API_URL}/act_{self.ad_account_id}/campaigns"
        params = {
            "access_token": self.access_token,
            "fields": "id,name,status,spend,impressions,clicks,actions"
        }
        
        try:
            response = requests.get(url, params=params)
            return response.json().get("data", [])
        except Exception as e:
            print(f"❌ خطأ في جلب الحملات: {e}")
            return []
    
    def get_campaign_insights(self, campaign_id):
        url = f"{META_API_URL}/{campaign_id}/insights"
        params = {
            "access_token": self.access_token,
            "fields": "spend,results,impressions,clicks,ctr,cpc",
            "date_preset": "today"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json().get("data", [])
            return data[0] if data else None
        except Exception as e:
            print(f"❌ خطأ في جلب الإحصائيات: {e}")
            return None
    
    def calculate_roi(self, spend, results):
        if spend == 0:
            return 0
        return float(results) / float(spend)
    
    def pause_campaign(self, campaign_id):
        url = f"{META_API_URL}/{campaign_id}"
        params = {
            "access_token": self.access_token,
            "status": "PAUSED"
        }
        
        try:
            response = requests.post(url, params=params)
            print(f"✅ تم إيقاف الحملة: {campaign_id}")
            return True
        except Exception as e:
            print(f"❌ خطأ في إيقاف الحملة: {e}")
            return False
    
    def increase_budget(self, campaign_id, increase_percent=20):
        url = f"{META_API_URL}/{campaign_id}"
        
        insights = self.get_campaign_insights(campaign_id)
        if not insights:
            return False
        
        current_spend = float(insights.get("spend", 0))
        new_budget = current_spend * (1 + increase_percent / 100)
        
        params = {
            "access_token": self.access_token,
            "daily_budget": int(new_budget * 100)
        }
        
        try:
            response = requests.post(url, params=params)
            print(f"✅ تم زيادة ميزانية الحملة: {campaign_id} بـ {increase_percent}%")
            return True
        except Exception as e:
            print(f"❌ خطأ في زيادة الميزانية: {e}")
            return False
    
    def monitor_and_optimize(self):
        print(f"\n📊 بدء المراقبة في {datetime.now()}")
        print("=" * 50)
        
        campaigns = self.get_campaigns()
        
        if not campaigns:
            print("❌ لا توجد حملات!")
            return
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "paused_campaigns": [],
            "boosted_campaigns": [],
            "stats": []
        }
        
        for campaign in campaigns:
            campaign_id = campaign.get("id")
            campaign_name = campaign.get("name")
            
            insights = self.get_campaign_insights(campaign_id)
            
            if not insights:
                continue
            
            spend = float(insights.get("spend", 0))
            results = float(insights.get("results", 0))
            roi = self.calculate_roi(spend, results)
            
            print(f"\n🎯 الحملة: {campaign_name}")
            print(f"   الإنفاق: {spend} جنيه")
            print(f"   النتائج: {results}")
            print(f"   ROI: {roi:.2f}")
            
            stats = {
                "campaign_name": campaign_name,
                "campaign_id": campaign_id,
                "spend": spend,
                "results": results,
                "roi": roi,
                "status": "active"
            }
            
            if roi < self.min_roi and spend > 100:
                print(f"   ⛔ ROI منخفض جداً! سيتم إيقاف الحملة")
                self.pause_campaign(campaign_id)
                stats["status"] = "paused"
                report["paused_campaigns"].append(campaign_name)
            
            elif roi > self.max_roi:
                print(f"   🚀 ROI عالي جداً! سيتم زيادة الصرف")
                self.increase_budget(campaign_id, increase_percent=25)
                report["boosted_campaigns"].append(campaign_name)
            
            report["stats"].append(stats)
        
        self.print_report(report)
        return report
    
    def print_report(self, report):
        print("\n" + "=" * 50)
        print("📋 التقرير اليومي")
        print("=" * 50)
        print(f"الوقت: {report['timestamp']}")
        print(f"الحملات الموقوفة: {len(report['paused_campaigns'])}")
        print(f"الحملات المعززة: {len(report['boosted_campaigns'])}")
        print("\nالحملات الموقوفة:")
        for camp in report['paused_campaigns']:
            print(f"  - {camp}")
        print("\nالحملات المعززة:")
        for camp in report['boosted_campaigns']:
            print(f"  - {camp}")
        print("=" * 50)

def main():
    manager = COZAAdManager(AD_ACCOUNT_ID, ACCESS_TOKEN)
    
    while True:
        manager.monitor_and_optimize()
        print("\n⏰ انتظار ساعة واحدة قبل المراقبة التالية...")
        time.sleep(3600)

if __name__ == "__main__":
    main()
