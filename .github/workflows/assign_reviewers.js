// assigns reviewers based on the category of the [Proposal] issue
const { Octokit } = require("@octokit/rest");

const org = "open-feature";
const repo = process.argv[2];
const prNumber = process.argv[3];
const category = process.argv[4];

async function assigner(repo, prNumber, team_Slugs_updated) {
    const octokit = new Octokit({
        auth: process.env.TOKEN
    });
    try {
        await octokit.pulls.requestReviewers({
        owner: repo.split("/")[0],
        repo: repo.split("/")[1],
        pull_number: prNumber,
        team_reviewers: team_Slugs_updated
        });
        console.log(`Teams assigned successfully.`);
    } catch (error) {
        console.error("An error occurred:", error);
    }
}

async function assignReviewers(org,repo, prNumber, category) {
  const octokit = new Octokit({
    auth: process.env.TOKEN
  });
  try {
    const { data: teams } = await octokit.request('GET /orgs/{org}/teams',({
      headers: {
        'X-GitHub-Api-Version': '2022-11-28'
      },
      org: org,
    }));

    if(teams.length === 0){
      console.log(`No team found for the organisation"${org}".`);
      return;
    }
    // assigns the Proposal issue with "SDK" or "Specification" category to all the "sdk-maintainers"
    if(["SDKs", "Specification"].includes(category)){
    const team_updated = teams.filter((team) => team.slug.startsWith("sdk") && team.slug.endsWith("maintainers"));
    const team_Slugs_updated = team_updated.map((team) => team.slug);
    assigner(repo, prNumber, team_Slugs_updated);
    } // assigns the Proposal issue with "OpenFeature Operator" or "Flagd" category to all the "cloud-native-maintainers"
     else if(["Flagd", "OpenFeature Operator"].includes(category)){
    const team_updated = teams.filter((team) => team.slug.startsWith("cloud-native") && team.slug.endsWith("maintainers"));
    const team_Slugs_updated = team_updated.map((team) => team.slug);
    assigner(repo, prNumber, team_Slugs_updated);
    }else {
          console.log(`No team found for the category "${category}".`);
        }
  }catch (error) {
    console.error("An error occurred:", error);
  }
}

assignReviewers(org, repo, prNumber, category);