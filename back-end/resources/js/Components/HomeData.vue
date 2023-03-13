<script setup>

    import { Line } from 'vue-chartjs';
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

    

    ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale);

    let name = 'LineChart';
    const chartkey = ref(0);
    
    let labels = [ "7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00" ];

    let chartData = {
        labels: labels,
        datasets: [
            {
                label: "Potencia",
                backgroundColor: '#fff',
                tension: 0.5,
                data: [],
                pointBackgroundColor: ["white"],
                pointRadius: [3]
            },
        ]
    }

    let chartOptions =  {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            xAxis: [{
                
            }]
        }
    }

    function getData() {
        // Aquí recogeríamos de la api los datos
        let data = ["5.0","10.0","15.5","25.0","30.0","34.2","46.1","60.6","75.5","85.4","65.5"];

        // Comprobamos el largo del dataset para ver cual es el último elemento
        chartData.datasets[0].data = data;
        chartData.datasets[0].pointBackgroundColor[data.length - 1] = 'red'

        //Renderizamos el componente de nuevo
        chartkey.value += 1;
    }

    onMounted(() => {
        getData()
    })
    
</script>

<template>
    <Line
        id="my-chart-id"
        :options="chartOptions"
        :data="chartData"
        :key="chartkey"
    />
</template>

<style>

</style>