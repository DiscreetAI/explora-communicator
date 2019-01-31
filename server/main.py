from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource


#Set up Flask application
application = Flask(__name__)
api = Api(application)

#Set up job dictionary, which has the following structure:

# jobs = {
#     'job1' : {
#         'dataset1': {
#             'round_num': <round number>
#             'dataset_stats': <dataset_stats>
#         }
#         ...
#     }
#     ...
# }

jobs = {}

def make_success_dict(job_uuid=None):
    """
    Helper method to return successful query.
    """
    if job_uuid:
        return {
            'status': 'success',
            'job_dict': jobs[job_uuid]
        }
    else:
        return {
            'status': 'success'
        }

def make_failure_dict(error_message):
    """
    Helper method to return failed query.
    """
    return {
        'status': 'failure',
        'message': error_message 
    }

class Dataset(Resource):
    """
    Class associated with requests for a specific dataset.
    """
    def post(self, job_uuid, dataset_uuid):
        """
        """
        try: 
            assert 'round_num' in request.json, "round_num not found!"
            assert 'dataset_stats' in request.json, "dataset_stats not found!"
            if job_uuid not in jobs:
                jobs[job_uuid] = {}
            jobs[job_uuid][dataset_uuid] = request.json
            return make_success_dict()
        except Exception as e:
            return make_failure_dict(str(e))

class Job(Resource):
    """
    Class associated with requests for a specific job. Includes getting 
    data for dataset or clearing its data from jobs dictionary.
    """
    def get(self, job_uuid):
        """
        Get data for job with given job_uuid from jobs dictionary.

        Return success status if job data were found, failure otherwise.
        """
        if job_uuid in jobs:
            return make_success_dict(job_uuid) 
        else:
            return make_failure_dict("Job with UUID {} doesn't exist.".format(job_uuid))

    def delete(self, job_uuid):
        """
        Clear training stats for dataset with given uuid from datasets
        dictionary.

        Return success status if dataset stats were deleted, failure otherwise.
        """
        if job_uuid in jobs:
            del jobs[job_uuid]
            return make_success_dict()
        else:
            return make_failure_dict("Job with UUID {} doesn't exist.".format(job_uuid))
        
class JobsList(Resource):
    """
    Class associated with requests for all jobs. Includes clearing all data 
    from jobs dictionary.
    """

    def delete(self):
        """
        Clear the entire datasets dictionary.

        Return success status assuming entries were deleted.
        """
        if jobs:
            jobs.clear()
            return make_success_dict()
        else:
            return make_failure_dict("Dictionary is already empty!")

## Setup the Api resource routing here
api.add_resource(JobsList, '/jobs')
api.add_resource(Job, '/jobs/<job_uuid>')
api.add_resource(Dataset, '/jobs/<job_uuid>/<dataset_uuid>')

if __name__ == '__main__':
    application.run(debug=True)
