
async function handle(){ 
    const input = document.getElementById('input');
    console.log(input.files[0])
    const formData = new FormData();
    formData.append('data', JSON.stringify({"street":"bajkal","area_ha":50,"mapping_year":2020,"altitude":50,"color_id":1,"ownership_type_id":1,"original_functional_utilization_id":6,"utilization_id":2,"area_size_id":3,"location_id":3,"degradation_level_id":2,"residentional_area_category_id":2,"settlement_id":1,"infrastructure_availability_id":2,"natural_and_architectural_value_id":1,"revitalization_id":1}));
    formData.append('files', input.files[0],input.files[0].name);
    console.log(formData)
    const response = await fetch('http://localhost:8000/brownfields/insert', {
        method: 'POST',
        headers: {
            'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZRVZjZ1l2XzdzM2c5Z29IZTRJYzN3Q1pXQ2FJX3JJVkZ2OXE5YUNZVWEwIiwicm9sZXMiOlsxLDIsMyw0XSwiYWRtaW4iOmZhbHNlLCJhY3RpdmUiOnRydWUsImV4cCI6MTY3NDI0NDY2OH0.LBe66mGg3Ej-UhC9uD1Jg4tb6ULCLrikwW5ijNeIrE8'},
        body: formData,
    }).catch(e => console.log(e))

    console.log("POST RESULT CLIENT");
    console.log(response);

}

const button = document.getElementById('button');
button.onclick = handle;