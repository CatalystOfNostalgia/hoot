//
//  ProductParser.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation

class ProductParser {
    let PRODUCT_NAME_KEY = "product"
    let PRODUCT_EMOTION_KEY = "emotions"
    let PRODUCT_IMAGE_URL_KEY = "imageURL"
    let PRODUCT_SUMMARY_KEY = "summary"
    let PRODUCT_COMMENTS_KEY = "comments"
    
    let COMMENT_RELEVANCY_KEY = "relevancy"
    let COMMENT_DATA_KEY = "comment"
    let COMMENT_EMOTIONS_KEY = "emotions"
    let COMMENT_RATING_KEY = "rating"
    
    func parseProducts(data: NSData) -> [Product] {
        var products:[Product] = []
        
        do {
            let json = try NSJSONSerialization.JSONObjectWithData(data, options: .AllowFragments)
            
        } catch {
            
        }
        
        return products
    }
}