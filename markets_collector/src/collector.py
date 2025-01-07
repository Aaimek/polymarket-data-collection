import requests
import json
import logging

from polymarket_schemas.event import Event
from polymarket_schemas.market import Market
from polymarket_schemas.outcome import Outcome
from polymarket_schemas.clob_reward import ClobReward

def collect_events_objects():
    logging.info("Collecting events objects")
    events_data = get_events_data()
    events, markets, outcomes, clob_rewards = pre_process_events_data(events_data)


    logging.info("All objects collected.")
    return events, markets, outcomes, clob_rewards

def get_events_data():
    r = requests.get("https://gamma-api.polymarket.com/events?limit=1&closed=false")
    response = r.json()

    return response

def pre_process_events_data(events_data):
    events_list = []
    markets_list = []
    outcomes = []
    clob_rewards_list = []
    
    for event in events_data:

        # Process the event
        event_id = event['id']
        event_object = preprocess_event(event)
        events_list.append(event_object)

        for market in event['markets']:
            market_id = market['id']

            # Process the market
            market_object = preprocess_market(market, event_id)
            markets_list.append(market_object)

            # Process all the outcomes in the market
            # NOTE: There is no for loop becore the outcomes are not specied as a list in the API response
            market_outcomes = preprocess_outcome(market, event_id)
            outcomes += market_outcomes

            # Process the all the clob rewards in the market
            for reward in market['clobRewards']:
                clob_reward_object = preprocess_clob_reward(reward, market_id)
                clob_rewards_list.append(clob_reward_object)

    return events_list, markets_list, outcomes, clob_rewards_list

def preprocess_event(event):
    event_object = Event(
        id=event['id'],
        ticker=event['ticker'],
        slug=event['slug'],
        title=event['title'],
        description=event['description'],
        start_date=event['startDate'],
        creation_date=event['creationDate'],
        end_date=event['endDate'],
        image_url=event['image'],
        icon_url=event['icon'],
        active=event['active'],
        closed=event['closed'],
        archived=event['archived'],
        is_new=event['new'],
        featured=event['featured'],
        restricted=event['restricted'],
        liquidity=event['liquidity'],
        volume=event['volume'],
        created_at=event['createdAt'],
        updated_at=event['updatedAt'],
        competitive=event['competitive'],
        enable_order_book=event['enableOrderBook'],
        neg_risk=event['enableNegRisk'],
        neg_risk_market_id=None,
        comment_count=event['commentCount']
    )

    return event_object


def preprocess_market(market, event_id):
    market_object = Market(
        id=market['id'],
        event_id=event_id,
        question=market['question'],
        condition_id=market['conditionId'],
        slug=market['slug'],
        resolution_source=market['resolutionSource'],
        start_date=market['startDate'],
        end_date=market['endDate'],
        image_url=market['image'],
        icon_url=market['icon'],
        description=market['description'],
        volume=market['volume'],
        active=market['active'],
        closed=market['closed'],
        market_maker_address=market['marketMakerAddress'],
        created_at=market['createdAt'],
        updated_at=market['updatedAt'],
        closed_time=None,
        is_new=market['new'],
        featured=market['featured'],
        submitted_by=market['submitted_by'],
        archived=market['archived'],
        resolved_by=market['resolvedBy'],
        restricted=market['restricted'],
        group_item_title=market['groupItemTitle'],
        group_item_threshold=market['groupItemThreshold'],
        question_id=market['questionID'],
        uma_end_date=None,
        enable_order_book=market['enableOrderBook'],
        order_price_min_tick_size=market['orderPriceMinTickSize'],
        order_min_size=market['orderMinSize'],
        uma_resolution_status=None,
        volume_num=market['volumeNum'],
        end_date_iso=market['endDateIso'],
        start_date_iso=market['startDateIso'],
        has_reviewed_dates=market['hasReviewedDates'],
        uma_bond=market['umaBond'],
        uma_reward=market['umaReward'],
        fpmm_live=False,
        volume_clob=market['volumeClob'],
        accepting_orders=market['acceptingOrders'],
        neg_risk=market['negRisk'],
        neg_risk_market_id=None,
        neg_risk_request_id=None,
        ready=market['ready'],
        funded=market['funded'],
        cyom=market['cyom'],
        pager_duty_notification_enabled=market['pagerDutyNotificationEnabled'],
        approved=market['approved'],
    )

    return market_object


def preprocess_outcome(market, market_id):
    outcomes_names = json.loads(market['outcomes'])
    outcomes_prices = json.loads(market['outcomePrices'])
    outcomes_clob_token_ids = json.loads(market['clobTokenIds'])

    outcomes_results_dicts = []

    if len(outcomes_names) == len(outcomes_prices) == len(outcomes_clob_token_ids):
        for i in range(len(outcomes_names)):
            outcome_object = Outcome(
                name=outcomes_names[i],
                outcome_price=outcomes_prices[i],
                clob_token_id=outcomes_clob_token_ids[i],
                market_id=market_id
            )

            outcomes_results_dicts.append(outcome_object)

    else:
        raise Exception("The lengths of outcomes_names, outcomes_prices, and outcomes_clob_token_ids do not match.")

    return outcomes_results_dicts

def preprocess_clob_reward(reward, market_id):
    clob_reward_object = ClobReward(
        market_id=market_id,
        condition_id=reward['conditionId'],
        asset_address=reward['assetAddress'],
        rewards_amount=reward['rewardsAmount'],
        rewards_daily_rate=reward['rewardsDailyRate'],
        start_date=reward['startDate'],
        end_date=reward['endDate'],
    )

    return clob_reward_object