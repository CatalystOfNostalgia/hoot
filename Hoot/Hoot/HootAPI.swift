//
//  HootAPI.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class HootAPI {
    
    func getInitialSuggestions() -> [String] {
        // TODO: Create an API end point to get some initial suggestions 
        
        return ["Deadpool", "Kung Fu Panda 3", "The Witch", "Star Wars: Episode VII - The Force Aawakens", "The Revenant", "Zootopia"]
    }
    
    func getSuggestions(searchText: String) -> [String]{
        return ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
    }
    
    
}