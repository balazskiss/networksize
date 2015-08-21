angular.module('networkSizeReport', ['ngAnimate', 'ui.bootstrap'])
  .controller('MainController', function($scope, $http, $timeout) {
  var ctrl = this;
  
  $scope.files = []
  $scope.selectedFile = null
  $scope.results = []
  $scope.isLoading = false
  
  var renderGraph = function(containerID, dataPoints) {
    var data = [];
    var dataSeries = { type: "line" };
    dataSeries.dataPoints = dataPoints;
    data.push(dataSeries);

    var chart = new CanvasJS.Chart(containerID, {
      zoomEnabled: true,
      animationEnabled: false,
      axisX:{
        labelAngle: 30
      },
      axisY :{
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
    console.log("Loading file: "+file)
    $scope.isLoading = true
    $scope.selectedFile = file
    $scope.results = []

    $http.get('/files/'+file).success(function(response) {
      $scope.results = null
      $scope.results = response.result
      $scope.isLoading = false
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

});