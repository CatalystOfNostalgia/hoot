//
//  TestData.swift
//  Hoot
//
//  Created by Eric Luan on 4/13/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

// Use this for test data when testing the app independently of the server 
class TestData {
    static func getTestData() -> [Product] {
        var products: [Product] = []
        let comment1 = Comment(emotions: "Happy, Sad, Joyful", comment: "Wtf bro. I'm so happy.", relevancy: 1.0, rating: 5.0, complexEmotions: "asdf")
        let comment2 = Comment(emotions: "Angry, Happy, Disgusted", comment: "Blehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", relevancy: 1.0, rating: 1.5, complexEmotions: "asdf")
        let comment3 = Comment(emotions: "Happy, Sad, Joyful", comment: "Wtf bro. I'm so happy.", relevancy: 1.0, rating: 4.5, complexEmotions: "asdf")
        let comment4 = Comment(emotions: "Angry, Happy, Disgusted", comment: "Blehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", relevancy: 1.0, rating: 2.3, complexEmotions: "asdf"
        )
        products.append(Product(name: "Shabazz", description: "It's shabazzin' amazing", imageURL: "https://i.imgur.com/XdOrZ7C.jpg", emotions: "Confused, Scared", comments: [comment1, comment2]))
        products.append(Product(name: "Shaq'in the Fool", description: "Javveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeeeJavveelllllllee McGeeeeeeee", imageURL: "http://ecx.images-amazon.com/images/I/21GJEQT398L.jpg", emotions: "Confused, Scared", comments: [comment3, comment4]))
        
        return products
    }
}