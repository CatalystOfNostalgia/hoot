//
//  ReviewViewController.swift
//  Hoot
//
//  Created by Eric Luan on 4/21/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ReviewViewController: UIViewController {

    //@IBOutlet weak var commentTextView: UITextView!
    //@IBOutlet weak var relevancyLabel: UILabel!
    //@IBOutlet weak var basicEmotionsLabel: UILabel!
    //@IBOutlet weak var complexEmotionsLabel: UILabel!

    
    var comment: String?
    var basicEmotionText: String?
    var complexEmotionText: String?
    var relevancy: Double?
    var rating: Double?
    
//    override func viewDidLoad() {
//        commentTextView.text = comment
//        //basicEmotionsLabel.text = basicEmotionText
//        //complexEmotionsLabel.text = complexEmotionText
//        setReviewStars(rating!)
//        guard let relevancyValue = relevancy where relevancy != nil else {
//            return
//        }
//        relevancyLabel.text = "Relevancy: " + String(relevancyValue)
//        super.viewDidLoad()
//    }
    
    func setReviewStars(rating: Double) {
        // TODO FILL THIS IN 
    }
}
