from models import CampaignData, OfferData, MemberOfferData, MemberData, ndb
import logging
from datetime import datetime, timedelta


class CampaignDataService(CampaignData):
    DEFAULT_CAMPAIGN_NAME = 'default_campaign'

    @classmethod
    def get_campaign_key(cls, campaign_name=DEFAULT_CAMPAIGN_NAME):
        return ndb.Key('CampaignData', campaign_name)

    @classmethod
    def save_campaign(cls, json_data, created_time):
        campaign_dict = json_data['campaign_details']
        offer_dict = json_data['offer_details']

        campaign_name = campaign_dict['name']
        campaign_budget = int(campaign_dict['money'])
        campaign_category = campaign_dict['category']
        campaign_convratio = int(campaign_dict['conversion_ratio'])
        campaign_period = campaign_dict['period']
        start_date = campaign_dict['start_date']

        offer_type = offer_dict['offer_type']
        offer_min_val = int(offer_dict['min_value'])
        offer_max_val = int(offer_dict['max_value'])
        offer_valid_till = offer_dict['valid_till']
        offer_mbr_issuance = offer_dict['member_issuance']

        # Check min and max value are in the range 1 to 10
        offer_min_val = offer_min_val if (offer_min_val in range(1, 11)) else 1
        offer_max_val = offer_max_val if (offer_max_val in range(1, 11)) else 10

        campaign = CampaignData(name=campaign_name, money=campaign_budget, category=campaign_category,
                                conversion_ratio=campaign_convratio, period=campaign_period, offer_type=offer_type,
                                max_per_member_issuance_frequency=offer_mbr_issuance, max_value=offer_max_val,
                                min_value=offer_min_val, valid_till=offer_valid_till, start_date=start_date)

        campaign.key = CampaignDataService.get_campaign_key(campaign_name)
        campaign_key = campaign.put()
        logging.info('campaign_key:: %s', campaign_key)

        # Calculating end date based on period value which is in weeks.
        end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=7 * int(campaign_period) - 1)
        end_date = end_date.strftime("%Y-%m-%d")
        logging.info("Start_date:: %s and end_date %s", start_date, end_date)
        offer_list = list()

        # Create offer for each value as surprise point in range min value to max value
        for each_value in range(offer_min_val, offer_max_val + 1):
            offer_name = "%s_%s" % (str(campaign_name), str(each_value))
            offer = OfferData(surprise_points=each_value, threshold=10, OfferNumber=offer_name,
                              OfferPointsDollarName=offer_name, OfferDescription=offer_name,
                              OfferType="Xtreme Redeem", OfferSubType="Item", OfferStartDate=start_date,
                              OfferStartTime="00:00:00", OfferEndDate=end_date, OfferEndTime="23:59:00",
                              OfferBUProgram_BUProgram_BUProgramName="BU - Apparel",
                              OfferBUProgram_BUProgram_BUProgramCost=0.00, ReceiptDescription="TELL-16289",
                              OfferCategory="Stackable", OfferAttributes_OfferAttribute_Name="MULTI_TRAN_IND",
                              OfferAttributes_OfferAttribute_Values_Value="N", Rules_Rule_Entity="Product",
                              Rules_Conditions_Condition_Name="PRODUCT_LEVEL",
                              Rules_Conditions_Condition_Operator="IN",
                              Rules_Conditions_Condition_Values_Value="SEARSLEGACY~801~608~14~1~1~1~93059",
                              RuleActions_ActionID="ACTION-1", Actions_ActionID="ACTION-1",
                              Actions_ActionName="XR",
                              Actions_ActionProperty_PropertyType="Tier",
                              Actions_ActionProperty_Property_Name="MIN",
                              Actions_ActionProperty_Property_Values_Value="0.01",
                              created_at=created_time)
            offer.key = ndb.Key('OfferData', offer_name)
            offer.campaign = campaign_key
            offer_key = offer.put()
            offer_list.append(offer)
            logging.info('offer created with key:: %s', offer_key)
        return offer_list


class MemberOfferDataService(MemberOfferData):
    @classmethod
    def create(cls, offer_entity, member_entity):
        member_offer_data = MemberOfferData(offer=offer_entity.key, member=member_entity.key, status=False)
        member_offer_data_key = member_offer_data.put()
        return member_offer_data_key
