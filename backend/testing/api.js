const FormData = require('form-data');
const axios = require('axios').default;

async function fn(token,data){
    const formData = new FormData();
    //const data = JSON.stringify({"street":"bajkal","area_ha":50,"mapping_year":2020,"altitude":50,"color_id":1,"ownership_type_id":1,"original_functional_utilization_id":6,"utilization_id":2,"area_size_id":3,"location_id":3,"degradation_level_id":2,"residentional_area_category_id":2,"settlement_id":1,"infrastructure_availability_id":2,"natural_and_architectural_value_id":1,"revitalization_id":1})
    formData.append('data', data)
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

fn()
    
