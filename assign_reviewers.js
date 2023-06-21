// assigns reviewers based on the category of the [Proposal] issue
const { Octokit } = require("@octokit/rest");

async function assignReviewers(org,repo, prNumber, category) {
  const octokit = new Octokit({
    auth: process.env.TOKEN
  });
  try {
    const { data: teams } = await octokit.request('GET /orgs/{org}/teams',({
      headers: {
        // authorization: auth.token,
        'X-GitHub-Api-Version': '2022-11-28'
      },
      org: org,
    }));

    if(teams.length == 0){
      console.log(`No team found for the organisation"${org}".`);
      return;
    }
    // assigns the Proposal issue with "SDK" or "Specification" category to all the "sdk-maintainers"
    if(category === "SDKs" || category === "Specification"){
    const team_updated = teams.filter((team) => team.slug.startsWith("sdk") && team.slug.endsWith("maintainers"));
    const team_Slugs_updated = team_updated.map((team) => team.slug);
    await octokit.pulls.requestReviewers({
      owner: repo.split("/")[0],
      repo: repo.split("/")[1],
      pull_number: prNumber,
      team_reviewers: team_Slugs_updated
    });
    console.log(`Teams assigned successfully.`);
    } // assigns the Proposal issue with "OpenFeature Operator" or "Flagd" category to all the "cloud-native-maintainers"
     else if(category == "OpenFeature Operator" || category == "Flagd"){
    const team_updated = teams.filter((team) => team.slug.startsWith("cloud-native") && team.slug.endsWith("maintainers"));
    const team_Slugs_updated = team_updated.map((team) => team.slug);
    await octokit.pulls.requestReviewers({
      owner: repo.split("/")[0],
      repo: repo.split("/")[1],
      pull_number: prNumber,
      team_reviewers: team_Slugs_updated
    });
    console.log(`Teams assigned successfully.`);
    }else {
          console.log(`No team found for the category "${category}".`);
        }
  }catch (error) {
    console.error("An error occurred:", error);
  }
}
const org = "open-feature";
const repo = process.argv[2];
const prNumber = process.argv[3];
const category = process.argv[4];

assignReviewers(org, repo, prNumber, category);