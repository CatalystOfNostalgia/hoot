//
//  ProductParser.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

// Handles parsing the JSON returned from the server
class ProductParser {
    
    // Useful JSON Keys for getting information
    let PRODUCT_NAME_KEY = "product_name"
    let PRODUCT_EMOTION_KEY = "sentic_values"
    let PRODUCT_IMAGE_URL_KEY = "image_url"
    let PRODUCT_SUMMARY_KEY = "sumy"
    let PRODUCT_COMMENTS_KEY = "comments"
    
    let COMMENT_RELEVANCY_KEY = "relevancy"
    let COMMENT_DATA_KEY = "text"
    let COMMENT_COMPOUND_EMOTIONS_KEY = "compound_emotions"
    let COMMENT_SENTIC_EMOTIONS_KEY = "sentic_emotions"
    let COMMENT_RATING_KEY = "rating"
    
    let COMPOUND_EMOTION_EMOTION_KEY = "compound_emotion"
    let COMPOUND_EMOTION_STRENGTH_KEY = "strength"
    
    // Parses the high level array of products
    func parseProducts(data: NSData) -> [Product] {
        var products:[Product] = []
        
        do {
            let json: NSArray = try NSJSONSerialization.JSONObjectWithData(data, options: .AllowFragments) as! NSArray
            for item in json {
                if let productJson = item as? [String: AnyObject]{
                    products.append(parseProduct(productJson)!)
                }
            }
            
        } catch {
            print("Error has occured")
            print(error)
        }
        return products
    }
    
    // Parses a single product
    func parseProduct(product: [String: AnyObject]) -> Product? {
        guard let productName = product[PRODUCT_NAME_KEY] as? String else {
            return nil
        }
        guard let productUrl = product[PRODUCT_IMAGE_URL_KEY] as? String else {
            return nil
        }
        guard let emotions = product[PRODUCT_EMOTION_KEY] as? [String] else {
            return nil
        }
        guard let comments = product[PRODUCT_COMMENTS_KEY] as? NSArray else {
            return nil
        }
        guard let productDescription = product[PRODUCT_SUMMARY_KEY] as? String else {
            return nil
        }
        
        let productComments = parseComments(comments)
        let productEmotions = emotions.joinWithSeparator(", ")
        return Product(name: productName, description: productDescription, imageURL: productUrl, emotions: productEmotions, comments: productComments)
    }
    
    // Parse the comments for a product
    func parseComments(comments: NSArray) -> [Comment] {
        var parsed_comments:[Comment] = []
        for comment in comments {
            guard let commentJson = comment as? [String: AnyObject] else {
                continue
            }
            guard let relevancy = commentJson[COMMENT_RELEVANCY_KEY] as? Double else {
                continue
            }
            guard let commentText = commentJson[COMMENT_DATA_KEY] as? String else {
                continue
            }
            guard let compoundEmotions = commentJson[COMMENT_COMPOUND_EMOTIONS_KEY] as? NSArray else {
                continue
            }
            guard let senticEmotions = commentJson[COMMENT_SENTIC_EMOTIONS_KEY] as? [String] else {
                continue
            }
            guard let commentRating = commentJson[COMMENT_RATING_KEY] as? Double else {
                continue
            }
            let complexEmotions = processComplexEmotions(compoundEmotions)
            let basicEmotions = senticEmotions.joinWithSeparator(", ")
            parsed_comments.append(Comment(emotions: basicEmotions, comment: commentText, relevancy: relevancy, rating: commentRating, complexEmotions: complexEmotions))
        }
        return parsed_comments
    }
    
    // Parse the complex emotions for a comment
    func processComplexEmotions(complexComments: NSArray) -> String {
        var complexEmotionString: [String] = []
        for complexEmotion in complexComments {
            guard let emotionDict = complexEmotion as? [String: AnyObject] else {
                continue
            }
            guard let emotionString = emotionDict[COMPOUND_EMOTION_EMOTION_KEY] as? String  else {
                continue
            }
            guard let emotionStrength = emotionDict[COMPOUND_EMOTION_STRENGTH_KEY] as? String else {
                continue
            }
            complexEmotionString.append(emotionStrength + " " + emotionString)
        }
        return complexEmotionString.joinWithSeparator(", ")
    }
}