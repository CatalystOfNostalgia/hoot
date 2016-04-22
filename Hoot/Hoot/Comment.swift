//
//  Comment.swift
//  Hoot
//
//  Created by Eric Luan on 4/3/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class Comment {
    var emotions: String
    var complexEmotions: String
    var comment: String
    var relevancy: Double
    var rating: Double
    
    init(emotions: String, comment: String, relevancy: Double, rating: Double, complexEmotions: String) {
        self.emotions = emotions
        self.comment = comment
        self.relevancy = relevancy
        self.rating = rating
        self.complexEmotions = complexEmotions
    }
}