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
    @IBOutlet weak var basicEmotionLabel: UILabel!
    @IBOutlet weak var complexEmotionLabel: UILabel!
    @IBOutlet weak var productTitleLabel: UILabel!
    
    var comment: Comment?
    var productTitle: String!
    
    override func viewDidLoad() {
        
        commentTextView.text = comment!.comment
        commentTextView.setContentOffset(CGPointZero, animated: false)
        
        productTitleLabel.text = productTitle
        relevancyLabel.text = "Relevancy: \(comment!.relevancy)"
        basicEmotionLabel.text = comment?.emotions
        complexEmotionLabel.text = comment?.complexEmotions
        
        var images = getImages()
        
        firstStarView.image  = images[0]
        secondStarView.image = images[1]
        thirdStarView.image  = images[2]
        fourthStarView.image = images[3]
        fifthStarView.image  = images[4]
    }
    
    
    func getImages() -> [UIImage] {
        var images = [UIImage](count: 5, repeatedValue: UIImage(named: "31x31_0")!)
        
        print("rating \(comment!.rating)")
        switch(comment!.rating) {
        case 1..<1.5:
            images[0] = UIImage(named: "31x31_1")!
            images[1] = UIImage(named: "31x31_1-5")!
            break
        case 1.5..<2:
            images[0] = UIImage(named: "31x31_1")!
            images[1] = UIImage(named: "31x31_1")!
            break
        case 2..<2.5:
            images[0] = UIImage(named: "31x31_2")!
            images[1] = UIImage(named: "31x31_2")!
            images[2] = UIImage(named: "31x31_2-5")!
            break
        case 2.5..<3:
            images[0] = UIImage(named: "31x31_2")!
            images[1] = UIImage(named: "31x31_2")!
            images[2] = UIImage(named: "31x31_2")!
            break
        case 3..<3.5:
            images[0] = UIImage(named: "31x31_3")!
            images[1] = UIImage(named: "31x31_3")!
            images[2] = UIImage(named: "31x31_3")!
            images[3] = UIImage(named: "31x31_3-5")!
            break
        case 3.5..<4:
            images[0] = UIImage(named: "31x31_3")!
            images[1] = UIImage(named: "31x31_3")!
            images[2] = UIImage(named: "31x31_3")!
            images[3] = UIImage(named: "31x31_3")!
            break
        case 4..<4.5:
            images[0] = UIImage(named: "31x31_4")!
            images[1] = UIImage(named: "31x31_4")!
            images[2] = UIImage(named: "31x31_4")!
            images[3] = UIImage(named: "31x31_4")!
            images[4] = UIImage(named: "31x31_4-5")!
            break
        case 4.5..<5:
            images[0] = UIImage(named: "31x31_4")!
            images[1] = UIImage(named: "31x31_4")!
            images[2] = UIImage(named: "31x31_4")!
            images[3] = UIImage(named: "31x31_4")!
            images[4] = UIImage(named: "31x31_4")!
            break
        default:
            images[0] = UIImage(named: "31x31_5")!
            images[1] = UIImage(named: "31x31_5")!
            images[2] = UIImage(named: "31x31_5")!
            images[3] = UIImage(named: "31x31_5")!
            images[4] = UIImage(named: "31x31_5")!
            break
        }
        
        return images
    }
}
