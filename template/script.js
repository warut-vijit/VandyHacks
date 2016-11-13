var canvas;
var ctx;
function plot_stock(data) {
    //where data is a json array of two-element [date, value] pairs
    //
    var time_series = data.substring(2,data.length-2).split("],[");
    for(var i=0;i<time_series.length;i++){
        time_series[i] = time_series[i].split(",");
    }
    var delta_x = canvas.width/time_series.length;
    var height = canvas.height;
    var date_start = Date.parse(time_series[0])
    var values = [];
    var max = 0;
    for(var i=0;i<time_series.length;i++){//Find maximum
        values.push(parseInt(time_series[i][1]));
        max = Math.max(parseInt(time_series[i][1]),max);
    }
    max *= 3/2;
    ctx.fillStyle="#00135A";
    ctx.font="20px Arial";

    ctx.fillText(Math.round(max/4),15,3*height/4+10);
    ctx.fillText(Math.round(max/2),15,height/2+10);
    ctx.fillText(Math.round(3*max/4),15,height/4+10);

    ctx.fillText(time_series[Math.floor(time_series.length/4)][0],Math.floor(time_series.length/4)*delta_x-45,height-10);
    ctx.fillText(time_series[Math.floor(time_series.length/2)][0],Math.floor(time_series.length/2)*delta_x-45,height-10);
    ctx.fillText(time_series[Math.floor(time_series.length*3/4)][0],Math.floor(time_series.length*3/4)*delta_x-45,height-10);

    ctx.lineWidth="1px"
    ctx.strokeStyle="#A5A5FE";
    for(var i=0;i<time_series.length;i++){
        ctx.beginPath();
        ctx.moveTo(delta_x*i,0);
        ctx.lineTo(delta_x*i,height);
        ctx.stroke();
    }
    for(var i=0;i<8;i++){
        ctx.beginPath();
        ctx.moveTo(0,i*height/8);
        ctx.lineTo(canvas.width,i*height/8);
        ctx.stroke();
    }
    ctx.beginPath();
    ctx.lineWidth="2px";
    ctx.strokeStyle="#FF0000";
    ctx.moveTo(0, height-height/max*values[0]);
    for(var i=0;i<values.length;i++){
        if(values[i]==0){ctx.stroke();ctx.beginPath();}
        else{ctx.lineTo(delta_x*i,height-height/max*values[i]);}
    }
    ctx.stroke();
}
function plot_sentiment(data){
    //where data is a json array of two element [date, value] pairs
    //
    var time_series = data.substring(2,data.length-2).split("],[");
    for(var i=0;i<time_series.length;i++){
        time_series[i] = time_series[i].split(",");
    }//time_series is a 2d array, with one internal array per day and internall array w/ date and sentiment
    var delta_x = canvas.width/time_series.length;
    var height = canvas.height;
    var date_start = Date.parse(time_series[0])
    var values = [];
    for(var i=0;i<time_series.length;i++){//Find maximum
        values.push(parseInt(time_series[i][1]));
    }
    ctx.beginPath();
    ctx.lineWidth="2px";
    ctx.strokeStyle="#00FF00";
    ctx.moveTo(0, height-height/max*values[0]);
    for(var i=0;i<values.length;i++){
        ctx.lineTo(delta_x*i,height-height/4*values[i]);
    }
    ctx.stroke();
}
function canvas_init(){
    canvas = document.getElementById("canvas");
    canvas.width=document.body.clientWidth*0.8;
    canvas.height=document.body.clientHeight*0.6;
    ctx = canvas.getContext('2d');
    console.log("Initiated");
}