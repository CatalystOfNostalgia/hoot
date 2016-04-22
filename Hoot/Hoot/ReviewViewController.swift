//
//  ReviewViewController.swift
//  Hoot
//
//  Created by Anthony Dario on 4/21/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ReviewViewController: UIViewController {

    // MARK: Outlets
    @IBOutlet weak var firstStarView: UIImageView!
    @IBOutlet weak var secondStarView: UIImageView!
    @IBOutlet weak var thirdStarView: UIImageView!
    @IBOutlet weak var fourthStarView: UIImageView!
    @IBOutlet weak var fifthStarView: UIImageView!
    @IBOutlet weak var commentTextView: UITextView!
    @IBOutlet weak var relevancyLabel: UILabel!
    
    var comment: Comment?
    
    override func viewDidLoad() {
        
        commentTextView.text = comment!.comment
        relevancyLabel.text = "Relevancy: \(comment!.relevancy)"
    }
}
