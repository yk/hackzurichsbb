__author__ = 'yk'

from firebase import firebase
import itertools
import logging

BASE = "https://hackzurichsbb.firebaseio.com"


def get_feedbacks_for_train(train_name):
    fb = firebase.FirebaseApplication(BASE, None)
    params = {
        "orderBy": '"name"',
        "equalTo": '"%s"' % (train_name)
    }
    result = fb.get('/feedback', None, params=params)
    if result is None:
        return []
    return list(result.values())


def get_aggregated_feedbacks_for_train(train_name):
    fbs = get_feedbacks_for_train(train_name)
    agg = itertools.groupby(fbs, key=lambda e: e['feedback'])
    return dict((k, len(list(v))) for k, v in agg)


def annotate_section(section):
    section['feedbackCounts'] = get_aggregated_feedbacks_for_train(section['journey']['name']) or {}


if __name__ == '__main__':
    logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    print(get_feedbacks_for_train("IR 2481"))
    print(get_aggregated_feedbacks_for_train("IR 2481"))
