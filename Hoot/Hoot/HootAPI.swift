//
//  HootAPI.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class HootAPI {
    
    func getInitialSuggestions() -> [Product] {
        // TODO: Create an API end point to get some initial suggestions 
        
        return TestData.getTestData()
    }
    
    func getSuggestions(searchText: String) -> [Product]{
        return TestData.getTestData()
    }
    
    
}