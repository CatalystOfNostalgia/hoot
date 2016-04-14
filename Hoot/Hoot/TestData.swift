//
//  TestData.swift
//  Hoot
//
//  Created by Eric Luan on 4/13/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class TestData {
    static func getTestData() -> [Product] {
        var products: [Product] = []
        let comment1 = Comment(emotions: "Happy, Sad, Joyful", comment: "Wtf bro. I'm so happy.", userName: "DudeKiller500")
        let comment2 = Comment(emotions: "Angry, Happy, Disgusted", comment: "Blehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", userName: "Joejoe2500")
        let comment3 = Comment(emotions: "Happy, Sad, Joyful", comment: "Wtf bro. I'm so happy.", userName: "DudeKiller500")
        let comment4 = Comment(emotions: "Angry, Happy, Disgusted", comment: "Blehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", userName: "Joejoe2500")
        products.append(Product(name: "Shabazz", description: "It's shabazzin' amazing", imageURL: "https://i.imgur.com/XdOrZ7C.jpg", emotions: "Confused, Scared", comments: [comment1, comment2]))
        products.append(Product(name: "Shaq'in the Fool", description: "Javveelllllllee McGeeeeeeee", imageURL: "https://i.imgur.com/7YZLrKu.jpg", emotions: "Confused, Scared", comments: [comment3, comment4]))
        
        return products
    }
}