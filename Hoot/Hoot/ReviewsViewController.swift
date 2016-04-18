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

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCellWithIdentifier("Cell") as! ReviewTableCell
        let index = indexPath.row
        if let relevancy = comments![index].relevancy {
            cell.relevancyLabel.text = "Relevancy: \(relevancy)"
        }
        cell.reviewTextPreview.text = comments![index].comment
        return cell 
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return (comments?.count)!
    }
}
