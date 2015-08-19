angular.module('networkSizeReport', ['ngAnimate', 'ui.bootstrap', 'chart.js'])
.controller('MainController', function($scope, $http, $timeout) {
    var ctrl = this;

    $scope.files = []
    $scope.selectedFile = null
    $scope.results = []

    $scope.loadFile = function(file) {
        $scope.selectedFile = file

        $http.get('/files/'+file).success(function(response) {
            $scope.results = null
            $scope.results = response.result
        });
    }

    $http.get('/files').success(function(response) {
        $scope.files = response.result
    });
    
    $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
    $scope.series = ['Series A', 'Series B'];
    $scope.data = [
      [65, 59, 80, 81, 56, 55, 40],
      [28, 48, 40, 19, 86, 27, 90]
    ];
    $scope.onClick = function (points, evt) {
      console.log(points, evt);
    };

    $scope.showEstimates = function() {
        $scope.lineChartShow = true
        $scope.labels = $scope.results.map(function(obj){return obj["Return N"]});
        $scope.series = ["Series A"];
        $scope.data = [$scope.results.map(function(obj){return obj["Estimate"]})];
    };
    
    $scope.hideLineChart = function() {
        $scope.lineChartShow = false
    };
    
    $scope.showNewNodes = function() {
        $scope.lineChartShow = true
        $scope.labels = $scope.results.map(function(obj){return obj["Return N"]});
        $scope.series = ["Series A"];
        $scope.data = [$scope.results.map(function(obj){return obj["Number of Nodes"]})];
    };

    
});