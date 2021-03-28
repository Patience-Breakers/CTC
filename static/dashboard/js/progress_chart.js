

      // var subject =["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"]
      var Progress = [,2,2.5,4,5,4,4]
      var week = [1,2,3,4,5,6,7]
      // var John	=[ 55,	45,	56,	87,	21,	52,	89,	65]
      // var Suresh =[55,	64,	90,	61,	58,	2]
      // var Ramesh=[	25,	54,	89,	76	,95	,87	,56	,74]
      // var Jessica	=[78,	55,	86,	63,	54,	89,	75,	45]
      // var Jennifer	=[58,	96,	78,	46,	96,	77,	83,	53]
      var ctx = document.getElementById("myChart");
      var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Month,
          datasets: [
            { 
              data: Progress,
              label : "Month",
              borderColor : "#3cba9f",
              fill : false
            },
            // { 
            //     data: Ramesh,
            //     label : "Ranesh",
            //     borderColor : "#c45850",
            //     fill : false
            // },
            // { 
            //     data: John,
            //     label : "John",
            //     borderColor : "#e8c3b9",
            //     fill : false
            // },
            // { 
            //     data: Jessica,
            //     label : "Jessica",
            //     borderColor : "#3cba9f",
            //     fill : false
            // },
            // { 
            //     data: Jennifer,
            //     label : "Jennifer",
            //     borderColor : "#8e5ea2",
            //     fill : false
            // }
          ]
        }
      });
      