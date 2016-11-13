var canvas;
var ctx;
var active = false;
var time_series_stock, time_series_sentiment;
var delta_x;
var date_start;
var values_stock,values_sentiments;
var max;
function import_stock(data) {
    //where data is a json array of two-element [date, value] pairs
    //
    active = true;
    time_series_stock = data.substring(2,data.length-2).split("],[");
    for(var i=0;i<time_series_stock.length;i++){
        time_series_stock[i] = time_series_stock[i].split(",");
    }
    delta_x = canvas.width/time_series_stock.length;
    height = canvas.height;
    date_start = Date.parse(time_series_stock[0])
    values_stock = [];
    max = 0;
    for(var i=0;i<time_series_stock.length;i++){//Find maximum
        values_stock.push(parseInt(time_series_stock[i][1]));
        max = Math.max(parseInt(time_series_stock[i][1]),max);
    }
    max *= 3/2;
    plot_stock();
}
function plot_stock(){
    ctx.fillStyle="#e5e5e5";
    ctx.fillRect(0,0,canvas.width,height);

    ctx.fillStyle="#00135A";
    ctx.font="20px Arial";

    ctx.fillText(Math.round(max/4),15,3*height/4+10);
    ctx.fillText(Math.round(max/2),15,height/2+10);
    ctx.fillText(Math.round(3*max/4),15,height/4+10);

    ctx.fillText(time_series_stock[Math.floor(time_series_stock.length/4)][0],Math.floor(time_series_stock.length/4)*delta_x-45,height-10);
    ctx.fillText(time_series_stock[Math.floor(time_series_stock.length/2)][0],Math.floor(time_series_stock.length/2)*delta_x-45,height-10);
    ctx.fillText(time_series_stock[Math.floor(time_series_stock.length*3/4)][0],Math.floor(time_series_stock.length*3/4)*delta_x-45,height-10);

    ctx.lineWidth="1px"
    ctx.strokeStyle="#A5A5FE";
    for(var i=0;i<time_series_stock.length;i++){
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
    ctx.moveTo(0, height-height/max*values_stock[0]);
    for(var i=0;i<values_stock.length;i++){
        if(values_stock[i]==0){ctx.stroke();ctx.beginPath();}
        else{ctx.lineTo(delta_x*i,height-height/max*values_stock[i]);}
    }
    ctx.stroke();
}
function import_sentiment(data){
    if(active){
        //where data is a json array of two element [date, value] pairs
        //
        time_series_sentiment = data.substring(2,data.length-2).split("],[");
        for(var i=0;i<time_series_sentiment.length;i++){
            time_series_sentiment[i] = time_series_sentiment[i].split(",");
        }//time_series_sentiment is a 2d array, with one internal array per day and internall array w/ date and sentiment
        var values_sentiments = [];
        for(var i=0;i<time_series_sentiment.length;i++){//Find maximum
            values_sentiments.push(parseInt(time_series_sentiment[i][1]));
        }
        plot_sentiment();
    }
}
function plot_sentiment(){
    ctx.beginPath();
    ctx.lineWidth="2px";
    ctx.strokeStyle="#00FF00";
    ctx.moveTo(0, height-height/max*values_sentiments[0]);
    for(var i=0;i<values_sentiments.length;i++){
        ctx.lineTo(delta_x*i,height-height/4*values_sentiments[i]);
    }
    ctx.stroke();
}
function canvas_init(){
    canvas = document.getElementById("canvas");
    canvas.width=document.body.clientWidth*0.8;
    canvas.height=document.body.clientHeight*0.6;
    ctx = canvas.getContext('2d');
}
var previous_node = null;
function getLocation(e){
    if(active){
        var x = e.clientX-canvas.offsetLeft;
        var y = e.clientY-canvas.offsetTop;
        var delta_x = canvas.width/time_series_stock.length;
        var active_node = Math.round(x/delta_x);
        if(active_node!=previous_node && values_stock[active_node]>0){
            plot_stock();
            ctx.fillStyle="#DD0000";
            ctx.fillRect(active_node*delta_x-4,height-height/max*values_stock[active_node]-4,8,8);
            ctx.fillStyle="#00135A";
            ctx.font="15px Arial";
            ctx.fillText(values_stock[active_node],active_node*delta_x,height-height/max*values_stock[active_node]-5);
            ctx.fillText(time_series_stock[active_node][0],active_node*delta_x,height-height/max*values_stock[active_node]-20);
            previous_node = active_node;
        }
    }
}