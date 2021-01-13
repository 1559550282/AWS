const AWS = require('aws-sdk')
const docClient = new AWS.DynamoDB.DocumentClient()
const { MetricUnit } = require('../lib/helper/models')
const { putMetric } = require('../lib/logging/logger')

let _cold_start = true
exports.putItemHandler = async (event, context) => {
	    let response
	    try {
		            if (_cold_start) {
				                await putMetric(name = 'ColdStart', unit = MetricUnit.Count, value = 1, { service: 'item_service', function_name: context.functionName })
				                _cold_start = false
				            }
		            if (event.httpMethod !== 'POST') {
				                await putMetric(name = 'UnsupportedHTTPMethod', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'put-item' })
				                throw new Error(`PutItem only accept POST method, you tried: ${event.httpMethod}`)
				            }

		    	    console.log('before put item'+ event)
		            const item = await putItem(event)
		    	    console.log('after put item')

		            response = {
				                statusCode: 200,
				                headers: {
							                'Access-Control-Allow-Origin': '*'
							            },
				              body: JSON.stringify(item)
				            }

		    	    console.log('before put success')
		            await putMetric(name = 'SuccessfulPutItem', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'put-item' })
		    	    console.log('after put success')
		        } catch (err) {
				        response = {
						            statusCode: 500,
						            headers: {
								                  'Access-Control-Allow-Origin': '*'
								              },
						          body: JSON.stringify(err)
						        }
				        await putMetric(name = 'FailedPutItem', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'put-item' })
				    }
	    return response
}

const putItem = async (event) => {
	    let response
	    try {

		    	    console.log('putItem')
		            const body = JSON.parse(event.body)
		            const id = body.id
		            const name = body.name
			console.log('id:'+id+' name:'+name + ' tableanem:'+process.env.SAMPLE_TABLE)
		            var params = {
				                TableName: process.env.SAMPLE_TABLE,
				                Item: { id: id, name: name }
				            }

		            response = await docClient.put(params).promise()

		        } catch (err) {
				console.log('put item error')
				        throw err
				    }
	    return response
}
