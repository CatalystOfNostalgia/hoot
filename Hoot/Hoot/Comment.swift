//
//  Comment.swift
//  Hoot
//
//  Created by Eric Luan on 4/3/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class Comment {
    var emotions: [Emotion]?
    var comment: String?
    var userName: String?
    var source: String?
    
    init(emotions: [Emotion], comment: String, userName: String, source: String) {
        self.emotions = emotions
        self.comment = comment
        self.userName = userName
        self.source = source
    }
}