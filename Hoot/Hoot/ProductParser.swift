//
//  ProductParser.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class ProductParser {
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
    
    func parseProduct(product: [String: AnyObject]) -> Product? {
        if let productName = product[PRODUCT_NAME_KEY] as? String {
            if let productUrl = product[PRODUCT_IMAGE_URL_KEY] as? String {
                if let emotions = product[PRODUCT_EMOTION_KEY] as? [String] {
                    if let comments = product[PRODUCT_COMMENTS_KEY] as? NSArray {
                        if let productDescription = product[PRODUCT_SUMMARY_KEY] as? String {
                            let productComments = parseComments(comments)
                            let productEmotions = emotions.joinWithSeparator(", ")
                            return Product(name: productName, description: productDescription, imageURL: productUrl, emotions: productEmotions, comments: productComments)
                    
                        }
                    }
                }
            }
        }
        
        return nil
    }
    
    func parseComments(comments: NSArray) -> [Comment] {
        var parsed_comments:[Comment] = []
        for comment in comments {
            if let commentJson = comment as? [String: AnyObject] {
                if let relevancy = commentJson[COMMENT_RELEVANCY_KEY] as? Double {
                    if let commentText = commentJson[COMMENT_DATA_KEY] as? String {
                        //if let compoundEmotions = commentJson[COMMENT_COMPOUND_EMOTIONS_KEY] as? [String] {
                            if let senticEmotions = commentJson[COMMENT_SENTIC_EMOTIONS_KEY] as? [String] {
                                if let commentRating = commentJson[COMMENT_RATING_KEY] as? Double {
                                    //var allEmotions = compoundEmotions.joinWithSeparator(",")
                                    var allEmotions = senticEmotions.joinWithSeparator(",")
                                    parsed_comments.append(Comment(emotions: allEmotions, comment: commentText, relevancy: relevancy, rating: commentRating))
                                }
                            }
                        //}
                    }
                }
            }
        }
        return parsed_comments
    }
}