import requests
import pytest
import json


@pytest.fixture(scope='session')
def good_job_uuid():
    return 'good_job_uuid'

@pytest.fixture(scope='session')
def good_dataset_uuid():
    return 'good_dataset_uuid'

@pytest.fixture(scope='session')
def sample_stats():
    return 'stats'

@pytest.fixture(scope='session')
def good_post_data(good_job_uuid, sample_stats):
    return {
        'round_num': 1,
        'dataset_stats': sample_stats
    }

@pytest.fixture(scope='session')
def bad_job_uuid():
    return 'bad_job_uuid'

@pytest.fixture(scope='session')
def bad_dataset_uuid():
    return 'bad_dataset_uuid'

@pytest.fixture(scope='session')
def base_url():
    return 'http://status-server.jn6tkty4uh.us-west-1.elasticbeanstalk.com/jobs'

@pytest.fixture(scope='session')
def job_url_format(base_url):
    return base_url + "/{job_uuid}"

@pytest.fixture(scope='session')
def good_job_url(job_url_format, good_job_uuid):
    return job_url_format.format(job_uuid=good_job_uuid)

@pytest.fixture(scope='session')
def good_dataset_url(good_job_url, good_dataset_uuid):
    return good_job_url + '/' + good_dataset_uuid

@pytest.fixture(scope='session')
def bad_job_url(base_url, bad_job_uuid):
    return base_url + '/' + bad_job_uuid

@pytest.fixture(scope='session')
def headers():
    return {'content-type': 'application/json'}

def test_post_and_get(good_dataset_uuid, sample_stats, good_post_data, \
        headers, good_job_url, good_dataset_url):
    """
    POST stats with a given job_uuid and check that GET retrieves those stats.
    """
    response = requests.post(
        url=good_dataset_url,
        headers=headers,
        json=good_post_data
    )
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "POST failed!"

    response = requests.get(good_job_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "GET failed!"
    
    job_dict = response_dict['job_dict']
    assert good_dataset_uuid in job_dict, \
        "Dataset with UUID {} not found!".format(good_dataset_uuid)

    dataset_dict = job_dict[good_dataset_uuid]
    assert 'dataset_stats' in dataset_dict and dataset_dict['dataset_stats'] == sample_stats, \
        "Correct stats not received!"
    assert 'round_num' in dataset_dict and dataset_dict['round_num'] == 1, \
        "Correct round not received!"

def test_delete(good_job_uuid, good_job_url):
    """
    DELETE the entry for the given job_uuid (posted in previous test), and check to
    make sure that GET fails.
    """
    response = requests.delete(good_job_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "DELETE failed!"

    response = requests.get(good_job_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "GET should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Job with UUID {} doesn't exist.".format(good_job_uuid), \
        "Error message was not correct!"

def test_bad_get_and_bad_delete(bad_job_uuid, bad_job_url):
    """
    Check to make sure that GETs and DELETEs with random job_uuids will always fail.
    """
    response = requests.get(bad_job_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "GET should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Job with UUID {} doesn't exist.".format(bad_job_uuid), \
        "Error message was not correct!"

    response = requests.delete(bad_job_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'failure', \
        "DELETE should have failed!"
    assert 'message' in response_dict and \
        response_dict['message'] == "Job with UUID {} doesn't exist.".format(bad_job_uuid), \
        "Error message was not correct!"

def test_mass_post_and_delete(good_job_uuid, good_post_data, headers, \
    job_url_format, good_dataset_uuid, base_url):
    for i in range(1,6):
        new_job_uuid = good_job_uuid + str(i)
        new_url = job_url_format.format(job_uuid=new_job_uuid)
        new_url += '/' + good_dataset_uuid
        response = requests.post(
            url=new_url,
            headers=headers,
            json=good_post_data
        )
        response_dict = json.loads(response.text)
        assert 'status' in response_dict and response_dict['status'] == 'success', \
            "POST failed!"

    response = requests.delete(base_url)
    response_dict = json.loads(response.text)
    assert 'status' in response_dict and response_dict['status'] == 'success', \
        "DELETE failed!"

    for i in range(1,6):
        new_job_uuid = good_job_uuid + str(i)
        new_url = job_url_format.format(job_uuid=new_job_uuid)
        response = requests.get(new_url)
        response_dict = json.loads(response.text)
        assert 'status' in response_dict and response_dict['status'] == 'failure', \
            "GET should have failed!"
        assert 'message' in response_dict and \
            response_dict['message'] == "Job with UUID {} doesn't exist.".format(new_job_uuid), \
            "Error message was not correct!"
