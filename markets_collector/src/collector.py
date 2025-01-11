import requests
import json
import logging

from polymarket_shared.schemas import Event, Market, Outcome, ClobReward

from polymarket_shared.database_conn.database_conn import DatabaseManager

from sqlalchemy.exc import SQLAlchemyError

def collect_and_push_events_objects():
    try:
        events, markets, outcomes, clob_rewards = collect_events_objects()
        push_events_objects(events, markets, outcomes, clob_rewards)
    except Exception as e:
        logging.error(f"Failed in collect_and_push_events_objects: {str(e)}", exc_info=True)
        raise

def push_events_objects(events, markets, outcomes, clob_rewards):
    logging.info("Starting to push objects to database")
    db = DatabaseManager()

    try:
        # Push events first since markets depend on them
        logging.info(f"Pushing {len(events)} events")
        with db.session_scope() as session:
            for event in events:
                session.merge(event)

        # Push markets second since outcomes and clob_rewards depend on them
        logging.info(f"Pushing {len(markets)} markets")
        with db.session_scope() as session:
            for market in markets:
                session.merge(market)

        # Push outcomes third
        logging.info(f"Pushing {len(outcomes)} outcomes")
        with db.session_scope() as session:
            for outcome in outcomes:
                session.merge(outcome)

        # Push clob rewards last
        logging.info(f"Pushing {len(clob_rewards)} clob rewards")
        with db.session_scope() as session:
            for reward in clob_rewards:
                session.merge(reward)

        logging.info("Finished pushing all objects to database")
    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {str(e)}")
        raise

def collect_events_objects():
    logging.info("Collecting events objects")
    events_data = get_events_data()
    events, markets, outcomes, clob_rewards = pre_process_events_data(events_data)


    logging.info("All objects collected.")
    return events, markets, outcomes, clob_rewards

def get_events_data():
    try:
        r = requests.get("https://gamma-api.polymarket.com/events?limit=10000&closed=false")
        r.raise_for_status()  # Raises an HTTPError for bad responses
        return r.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch events data: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {str(e)}")
        raise

def pre_process_events_data(events_data):
    events_list = []
    markets_list = []
    outcomes = []
    clob_rewards_list = []
    
    for event in events_data:
        try:
            event_id = event['id']
            
            # Process the event
            try:
                event_object = preprocess_event(event)
                events_list.append(event_object)
            except KeyError as e:
                logging.error(f"Missing key while processing event {event_id}: {str(e)}")
                continue
            except Exception as e:
                logging.error(f"Error processing event {event_id}: {str(e)}")
                continue

            # Process markets for this event
            for market in event['markets']:
                try:
                    market_id = market['id']
                    market_object = preprocess_market(market, event_id)
                    markets_list.append(market_object)

                    # Process outcomes
                    try:
                        market_outcomes = preprocess_outcome(market, market_id)
                        outcomes.extend(market_outcomes)
                    except Exception as e:
                        logging.error(f"Error processing outcomes for market {market_id}: {str(e)}")
                        continue

                    # Process clob rewards
                    for reward in market.get('clobRewards', []):
                        try:
                            clob_reward_object = preprocess_clob_reward(reward, market_id)
                            clob_rewards_list.append(clob_reward_object)
                        except Exception as e:
                            logging.error(f"Error processing clob reward for market {market_id}: {str(e)}")
                            continue

                except KeyError as e:
                    logging.error(f"Missing key while processing market in event {event_id}: {str(e)}")
                    continue
                except Exception as e:
                    logging.error(f"Error processing market in event {event_id}: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"Error processing event data: {str(e)}")
            continue

    if not any([events_list, markets_list, outcomes, clob_rewards_list]):
        raise ValueError("No data was successfully processed")

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
    outcomes_clob_token_ids = json.loads(market['clobTokenIds'])

    outcomes_results_dicts = []

    if len(outcomes_names) == len(outcomes_clob_token_ids):
        for i in range(len(outcomes_names)):
            outcome_object = Outcome(
                name=outcomes_names[i],
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