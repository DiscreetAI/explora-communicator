from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource


#Set up Flask application
application = Flask(__name__)
api = Api(application)

#Set up dataset dictionary, which maps uuids to training stats
datasets = {}

def make_success_dict(stats=None):
    """
    Helper method to return successful query.
    """
    if stats:
        return {
            'status': 'success',
            'dataset_stats': stats
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
    Class associated with requests for a specific dataset. Includes getting 
    training stats for dataset or clearing its stats from datasets dictionary.
    """
    def get(self, uuid):
        """
        Get training stats for dataset with given uuid from datasets dictionary.

        Return success status if dataset stats were found, failure otherwise.
        """
        if uuid in datasets:
            return make_success_dict(datasets[uuid]) 
        else:
            return make_failure_dict("Dataset {} doesn't exist.".format(uuid))

    def delete(self, uuid):
        """
        Clear training stats for dataset with given uuid from datasets
        dictionary.

        Return success status if dataset stats were deleted, failure otherwise.
        """
        if uuid in datasets:
            del datasets[uuid]
            return make_success_dict()
        else:
            return make_failure_dict("Dataset {} doesn't exist.".format(uuid))
        
class DatasetList(Resource):
    """
    Class associated with requests for all dataset. Includes storing training 
    stats for specific dataset or clearing all stats from datasets dictionary.
    """

    def post(self):
        """
        Store training stats for given uuid in datasets dictionary.

        Return success status assuming storage was successful.
        """
        args = request.json
        uuid = args['uuid']
        stats = args['stats']
        datasets[uuid] = stats
        return make_success_dict()

## Setup the Api resource routing here
api.add_resource(DatasetList, '/datasets')
api.add_resource(Dataset, '/datasets/<uuid>')

if __name__ == '__main__':
    application.run(debug=True)
