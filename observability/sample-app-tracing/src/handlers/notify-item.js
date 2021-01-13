const AWSXRay = require('aws-xray-sdk-core')
const AWS = AWSXRay.captureAWS(require('aws-sdk'))

exports.notifiyNewItemHandler = async (event, context) => {
  let response
  try {
    const record = JSON.parse(event.Records[0].Sns.Message)
    response = await getItem(record)
  } catch (err) {
    throw err
  } 
  return response
}


const getItem = async (record) => {
  let response
  try {
    response = JSON.stringify(record)
  } catch (err) {
    throw err
  } 
  return response
}
