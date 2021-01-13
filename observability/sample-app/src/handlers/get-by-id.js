const AWS = require('aws-sdk')
const docClient = new AWS.DynamoDB.DocumentClient()
const { MetricUnit } = require('../lib/helper/models')
const { logMetric } = require('../lib/logging/logger')

let _cold_start = true

exports.getByIdHandler = async (event, context) => {
  let response, id
  try {
	  if (_cold_start) {
	await logMetric(name = 'ColdStart', unit = MetricUnit.Count, value = 1, { service: 'item_service', function_name: context.functionName })
		          _cold_start = false
		      }
    if (event.httpMethod !== 'GET') {
	    await logMetric(name = 'UnsupportedHTTPMethod', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'get-by-id' })
	      throw new Error(`getById only accept GET method, you tried: ${event.httpMethod}`)
      throw new Error(`getById only accept GET method, you tried: ${event.httpMethod}`)
    }

    id = event.pathParameters.id
    const item = await getItemById(id)

    response = {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(item)
    }
	  await logMetric(name = 'SuccessfulGetItem', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'get-by-id' })
  } catch (err) {
    response = {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(err)
    }
  }
	await logMetric(name = 'FailedGetItem', unit = MetricUnit.Count, value = 1, { service: 'item_service', operation: 'get-by-id' })
  return response
}


const getItemById = async (id) => {
  let response
  try {
    var params = {
      TableName: process.env.SAMPLE_TABLE,
      Key: { id: id }
    }

    response = await docClient.get(params).promise()
  } catch (err) {
    throw err
  }
  return response
}
