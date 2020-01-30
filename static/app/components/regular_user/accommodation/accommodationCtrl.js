(function(angular) {
    let app = angular.module("app");

    app.controller("AccommodationCtrl", [
        "$http",
        "$scope",
        function($http, $scope) {
            let that = this;

            this.accommodations = [];
            this.cities = [];

            this.selected = 1688169087;

            $scope.isReadonly = true;
            $scope.unavailableCounter = 0;

            this.getAccommodations = function(id) {
                $http.get("/api/accommodation/city/" + id).then(
                    function(response) {
                        console.log(response);
                        that.accommodations = response.data;
                        if (that.accommodations.length == 0) {
                            console.log("No accommodation for " + id);
                            $scope.unavailableCounter = 0;
                        } else {
                            for (let accommodation of that.accommodations) {
                                if (accommodation.available == 0) {
                                    $scope.unavailableCounter++;
                                }
                            }
                        }

                        that.getImages();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getCities = function() {
                $http.get("/api/cities").then(
                    function(response) {
                        console.log(response);
                        that.cities = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getImages = function() {
                $http.get("api/accommodation/images").then(
                    function(response) {
                        console.log(response);
                        this.images = response.data;

                        for (let accommodation of that.accommodations) {
                            accommodation.images = [];
                            for (let image of images) {
                                if (accommodation.name == image.name) {
                                    accommodation.images.push(image.path);
                                }
                            }
                        }
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAccommodations(this.selected);
            this.getCities();
        }
    ]);
})(angular);
