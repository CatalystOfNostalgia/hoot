//
//  ProductViewController.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

// Controls the detailed view for a single product
class ProductViewController: UIViewController {


    @IBOutlet weak var productName: UILabel!
    @IBOutlet weak var summary: UITextView!
    @IBOutlet weak var image: UIImageView!
    @IBOutlet weak var emotions: UILabel!
    
    var comments:[Comment]?
    var summaryText: String?
    var productImage: UIImage?
    var emotionText: String?
    var product: String?
    
    // MARK: Navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "ShowReviews" {
            if let destination = segue.destinationViewController as? ReviewsViewController {
                destination.comments = comments
                destination.productTitle = product
            }
        }
    }
    
    // MARK: Controlling the view
    override func viewDidLoad() {

        self.summary.text = summaryText
        self.image.image = productImage
        self.productName.text = product
        self.emotions.text = emotionText
    }
    
    override func viewDidLayoutSubviews() {
        self.summary.setContentOffset(CGPointZero, animated: false)
    }
    
    @IBAction func viewComments(sender: AnyObject) {
        // Unnecessary to implement this function because of below functions.
    }
    
}
