//
//  HootAPI.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class HootAPI {
    var products: [Product] = []
    
    func getSuggestions(searchText: String?, emotionText: String?) -> [Product]{
        return TestData.getTestData()
    }
    
    // TODO: Replace current geSuggestions() with this once this is ready.
    func getRealSuggestions(searchText: String?, emotionText: String?, completionHandler: (([Product]?, NSError!) -> Void)!) -> Void {
        var searchString = APIConfigs().baseURL + APIConfigs().searchEndPoint
        
        // Determiens what kind of search we should do
        if searchText == nil && emotionText == nil{
            // Do Nothing
        } else if searchText == nil {
            searchString = searchString + "?" + APIConfigs().emotionKey + "=" + emotionText!
        } else if emotionText == nil {
            searchString = searchString + "?" + APIConfigs().queryKey + "=" + searchText!
        } else {
            searchString = searchString + "?" + APIConfigs().emotionKey + "=" + emotionText! + "&" + APIConfigs().queryKey + "=" + searchText!
        }
        let url: NSURL = NSURL(string: searchString.stringByAddingPercentEscapesUsingEncoding(NSUTF8StringEncoding)!)!
        let sessionConfiguartion: NSURLSessionConfiguration = NSURLSessionConfiguration.defaultSessionConfiguration()
        let session: NSURLSession = NSURLSession(configuration: sessionConfiguartion)
        print(url.description)
        let dataTask = session.dataTaskWithURL(url) {
            data, response, error in
            if error != nil {
                completionHandler(nil, error)
                print("Error retrieveing from server")
                print(error?.code)
                return
            } else {
                // TODO: Handle proper response
                completionHandler(ProductParser().parseProducts(data!), nil)
            }
            
        }
        print("Task dispatched")
        print(searchString)
        dataTask.resume()
    }
    
}