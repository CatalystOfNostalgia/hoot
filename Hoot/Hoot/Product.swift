//
//  Product.swift
//  Hoot
//
//  Created by Eric Luan on 4/3/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class Product {
    var name: String?
    var description: String?
    var imageURL: String?    
    var emotions: String?
    var comments: [Comment]?
    
    init(name: String, description: String, imageURL: String, emotions: String, comments: [Comment]) {
        self.name = name
        self.imageURL = imageURL
        self.description = description
        self.emotions = emotions
        self.comments = comments
    }
    
    
}