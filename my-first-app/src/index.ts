
import { Probot } from "probot";

export = ({ app }: { app: Probot }) => {
  // app.on("issues.opened", async (context) => {
  //   app.log.info("issue open",context);
  //   console.log("print ",context)
  //   const issueComment = context.issue({
  //     body: "Thanks for opening this issue!",
  //   });
  //   // Post a comment on the issue
  //   return context.octokit.issues.createComment(issueComment);
  // });
hello

  app.on(['pull_request.closed', 'pull_request.synchronize'], async (context) => {
    // An issue was edited, what should we do with it?
    app.log.info("issue open",context);
    const params = context.issue({body: 'success'})
   
    // const number = context.pullRequest.call.name.
   
    // Post a comment on the issue
    // return context.octokit.pullRequests.createComment(pullComment) 
    return context.github.issues.createComment(params)
  });

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
};


