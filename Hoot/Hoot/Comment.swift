//
//  Comment.swift
//  Hoot
//
//  Created by Eric Luan on 4/3/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class Comment {
    var emotions: String?
    var comment: String?
    var userName: String?
    
    init(emotions: String, comment: String, userName: String) {
        self.emotions = emotions
        self.comment = comment
        self.userName = userName
    }
}