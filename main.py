get("name")
            
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
            
            # إذا كان ROI منخفض جداً = إيقاف الحملة
            if roi < self.min_roi and spend > 100:
                print(f"   ⛔ ROI منخفض جداً! سيتم إيقاف الحملة")
                self.pause_campaign(campaign_id)
                stats["status"] = "paused"
                report["paused_campaigns"].append(campaign_name)
            
            # إذا كان ROI عالي جداً = زيادة الصرف
            elif roi > self.max_roi:
                print(f"   🚀 ROI عالي جداً! سيتم زيادة الصرف")
                self.increase_budget(campaign_id, increase_percent=25)
                report["boosted_campaigns"].append(campaign_name)
            
            report["stats"].append(stats)
        
        # طباعة التقرير
        self.print_report(report)
        return report
    
    def print_report(self, report):
        """طباعة التقرير اليومي"""
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
    """البرنامج الرئيسي"""
    manager = COZAAdManager(AD_ACCOUNT_ID, ACCESS_TOKEN)
    
    # شغل المراقبة كل ساعة
    while True:
        manager.monitor_and_optimize()
        print("\n⏰ انتظار ساعة واحدة قبل المراقبة التالية...")
        time.sleep(3600)  # ساعة واحدة

if name == "__main__":
    main()
