//
//  ReviewsViewController.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ReviewsViewController: UITableViewController {
    var comments: [Comment]?
    var selectedRow: Int?
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCellWithIdentifier("Cell") as! ReviewTableCell
        let index = indexPath.row
        cell.relevancyLabel.text = "Relevancy: \(comments![index].relevancy)"
        cell.reviewTextPreview.text = comments![index].comment
        cell.reviewTextPreview.setContentOffset(CGPointZero, animated: false)
        return cell
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return (comments?.count)!
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        selectedRow = indexPath.row
        performSegueWithIdentifier("GoToReview", sender: self)
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "GoToReview" {
            if let destination = segue.destinationViewController as? ReviewViewController {
                let comment = comments![selectedRow!]
                destination.comment = comment.comment
                destination.basicEmotionText = comment.emotions
                destination.complexEmotionText = comment.emotions
                destination.relevancy = comment.relevancy
                destination.rating = comment.rating
            }
        }
    }
}
