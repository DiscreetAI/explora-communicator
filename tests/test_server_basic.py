import requests
import pytest
import json


@pytest.fixture(scope='session')
def good_uuid():
    return 'good_uuid'

@pytest.fixture(scope='session')
def sample_stats():
    return 'stats'

@pytest.fixture(scope='session')
def good_post_data(good_uuid, sample_stats):
    return {
        'uuid': good_uuid,
        'dataset_stats': sample_stats
    }

@pytest.fixture(scope='session')
def bad_uuid():
    return 'bad_uuid'

@pytest.fixture(scope='session')
def base_url():
    return 'http://status-server.jn6tkty4uh.us-west-1.elasticbeanstalk.com/datasets'

@pytest.fixture(scope='session')
def good_dataset_url(base_url, good_uuid):
    return base_url + '/' + good_uuid

@pytest.fixture(scope='session')
def bad_dataset_url(base_url, bad_uuid):
    return base_url + '/' + bad_uuid

@pytest.fixture(scope='session')
def headers():
    return {'content-type': 'application/json'}

def test_post_and_get(sample_stats, good_post_data, headers, base_url, good_dataset_url):
    """
    POST stats with a given uuid and check that GET retrieves those stats.
    """
    response = requests.post(
        url=base_url,
        headers=headers,
        json=good_post_data
    )
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "POST failed!"

    response = requests.get(good_dataset_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "GET failed!"
    assert 'dataset_stats' in response_dict and response_dict['dataset_stats'] == sample_stats, \
        "Unexpected stats received!"

def test_delete(good_uuid, good_dataset_url):
    """
    DELETE the entry for the given uuid (posted in previous test), and check to
    make sure that GET fails.
    """
    response = requests.delete(good_dataset_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "DELETE failed!"

    response = requests.get(good_dataset_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "GET should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Dataset with UUID {} doesn't exist.".format(good_uuid), \
        "Error message was not correct!"

def test_bad_get_and_bad_delete(bad_uuid, bad_dataset_url):
    """
    Check to make sure that GETs and DELETEs with random UUIDs will always fail.
    """
    response = requests.get(bad_dataset_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "GET should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Dataset with UUID {} doesn't exist.".format(bad_uuid), \
        "Error message was not correct!"

    response = requests.delete(bad_dataset_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "GET should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Dataset with UUID {} doesn't exist.".format(bad_uuid), \
        "Error message was not correct!"



    
