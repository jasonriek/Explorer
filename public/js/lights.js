async function controlLed(light, action) {
    try {
        const response = await fetch(`/control-led/${light}/${action}`, {
            method: 'POST'
        });
        const result = await response.text();
        console.log(result);
    } catch (error) {
        console.log('Error controlling LED');
    }
}