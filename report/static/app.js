angular.module('networkSizeReport', ['ngAnimate', 'ui.bootstrap'])
  .controller('MainController', function($scope, $http, $timeout) {
  var ctrl = this;

  $scope.files = []
  $scope.selectedFile = null
  $scope.results = []
  $scope.degDist = null
  $scope.isLoading = false

  // Sockets
  namespace = '';
  var socket = io.connect('http://' + document.domain + ':' + 5001 + namespace);

  socket.on('connect', function() {
    console.log("connect");
    socket.emit('connect');
  });

  socket.on('filesWatcher', function(msg) {
    console.log(msg);
    if($scope.selectedFile == msg.src) {
      $scope.loadFile($scope.selectedFile)
    }
  });

  // Utility
  var getDegDistFileName = function(file) {
    return file.replace(/\.[^/.]+$/, ".degdist.json");
  }
  
  var refreshView = function() {
    var tab = $('.nav-tabs .active').text().trim()
    console.log(tab)
    if(tab == "Data") {
    }else if(tab == "Estimate"){
      $scope.showEstimates()
    }else if(tab == "New Nodes"){
      $scope.showNewNodes()
    }else if(tab == "Degree Distribution"){
      $scope.showDegrees()
    }
  }

  var renderGraph = function(containerID, dataPoints) {
    var data = [];
    var dataSeries = { type: "line" };
    dataSeries.dataPoints = dataPoints;
    data.push(dataSeries);

    var maxX = parseInt(dataPoints[0].x)
    for(var i=0; i < dataPoints.length; i++){
      if (maxX < parseInt(dataPoints[i].x)) {
        maxX = parseInt(dataPoints[i].x)
      }
    }

    var chart = new CanvasJS.Chart(containerID, {
      zoomEnabled: true,
      animationEnabled: false,
      axisX: {
        labelAngle: 30,
        maximum: maxX
      },
      axisY: {
        includeZero:false
      },
      data: data
    });

    $timeout( function(){ chart.render(); }, 100);
  }

  $http.get('/files').success(function(response) {
    $scope.files = response.result
  });

  $scope.loadFile = function(file) {
    if($scope.isLoading) return;
    console.log("Loading file: "+file)
    $scope.isLoading = true
    $scope.selectedFile = file
    $scope.results = []
    $scope.degDist = null

    $http.get('/files/'+file).success(function(response) {
      $scope.results = response.result
      $scope.isLoading = false
      refreshView()
    });

    $http.get('/files/'+getDegDistFileName(file)).success(function(response) {
      $scope.degDist = response.result
      refreshView()
    });
  }

  $scope.showEstimates = function() {
    var dataPoints = [];
    for (var i = 0; i < $scope.results.length; i++) {
      dataPoints.push({
        x: parseInt($scope.results[i]["Return N"]),
        y: parseInt($scope.results[i]["Estimate"])
      });
    }
    renderGraph("estimatesChart", dataPoints);
  };

  $scope.showNewNodes = function() {
    var dataPoints = [];
    for (var i = 0; i < $scope.results.length; i++) {
      dataPoints.push({
        x: parseInt($scope.results[i]["Return N"]),
        y: parseInt($scope.results[i]["Number of Nodes"])
      });
    }
    renderGraph("newNodesChart", dataPoints);
  };

  $scope.showDegrees = function() {
    if($scope.degDist == null) { return }
    var data = JSON.parse($scope.degDist)
    var dataPoints = [];
    for (var key in data) {
      dataPoints.push({
        x: key,
        y: data[key]
      });
    }
    renderGraph("degreesChart", dataPoints);
  };

});