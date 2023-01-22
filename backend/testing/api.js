const FormData = require('form-data');
const axios = require('axios').default;
const fs = require('fs/promises');

async function fn(token,data){
    const formData = new FormData();
    const image_1 = await fs.readFile('./images/img_1.jpg');
    const image_2 = await fs.readFile('./images/img_2.jpg');
    formData.append('data', data)
    formData.append('files',image_1,'image_1.jpg')
    formData.append('files',image_2,'image_2.jpg')
    const options = {
        method: 'POST',
        url: 'http://localhost:8000/brownfields/insert',
        headers: {
            'Authorization' : 'Bearer '+token,
            'Content-Type': 'multipart/form-data'
        },
        data: formData
    }
    
    axios.request(options)
}

const data = JSON.stringify({"street":"AERO","area_ha":50,"mapping_year":2020,"altitude":50,"color_id":1,"ownership_type_id":1,"original_functional_utilization_id":6,"utilization_id":2,"area_size_id":3,"location_id":3,"degradation_level_id":2,"residentional_area_category_id":2,"settlement_id":1,"infrastructure_availability_id":2,"natural_and_architectural_value_id":1,"revitalization_id":1})
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1bngyZHVPdnY2a2o5QTFoYWt3MWQ4ODZCX0xmSW1aZThkdHdkRjNyTFBvIiwicm9sZXMiOlsxLDIsMyw0XSwiYWRtaW4iOmZhbHNlLCJhY3RpdmUiOnRydWUsImV4cCI6MTY3NDIxNDE1MH0.0XnwLpV1QV4OeqBm0v2H6dV5sNbVJ2OmwKry8-NzU_Y'
fn(token,data)
    
