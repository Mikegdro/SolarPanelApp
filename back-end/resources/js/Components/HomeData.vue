<script>

    import { Line } from 'vue-chartjs'

    import {
        Chart as ChartJS,
        CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Legend,
    } from 'chart.js'

    ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale)

    function getLabels() {
        
    }

    function getData() {

    }
    
    export default{
        name: 'LineChart',
        components: { Line },
        data() {
            return {
                data: {
                    labels: getLabels(),
                    datasets: [
                        {
                            backgroundColor: '#f87979',
                            tension: 0.5,
                            data: getData()
                        }
                    ]
                },
                options: {
                    
                    responsive: true,
                    maintainAspectRatio: true
                }
            }
        }
    }
</script>

<template>
    <Line
        id="my-chart-id"
        :options="options"
        :data="data"
    />
</template>