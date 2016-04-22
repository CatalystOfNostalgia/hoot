//
//  SearchResultTableCell.swift
//  Hoot
//
//  Created by Eric Luan on 4/3/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit
import Foundation

class SearchResultTableCell: UITableViewCell {
    
    @IBOutlet weak var secondaryLabel: UILabel! // Used for displaying meta data
    @IBOutlet weak var mainLabel: UILabel! // Used for displaying the actual title of the search result
    @IBOutlet weak var thumbnail: UIImageView! // Used for displaying a thumbnail of the search result 
    
    var product: Product?
    
    func setValues() {
        guard let _ = product where product != nil else {
            return
        }
        
        mainLabel.text = product?.name
        secondaryLabel.text = product?.description
        let url = NSURL(string: (product?.imageURL)!)
        downloadImage(url!)
        
    }
    
    func getData(url:NSURL, completion: ((data: NSData?, response: NSURLResponse?, error: NSError? ) -> Void)) {
        NSURLSession.sharedSession().dataTaskWithURL(url) { (data, response, error) in
            completion(data: data, response: response, error: error)
            }.resume()
    }
    
    func downloadImage(url: NSURL){
        getData(url) { (data, response, error)  in
            dispatch_async(dispatch_get_main_queue()) { () -> Void in
                guard let data = data where error == nil else {
                    // Something went wrong getting the image out 
                    self.thumbnail.image = UIImage(named: "NoImage.png")
                    return
                }
                self.thumbnail.image = UIImage(data: data)
            }
        }
    }
    
    
}
