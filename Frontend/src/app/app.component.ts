import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from 'src/model/api.service';
import { TeamInfo } from 'src/model/model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private apiService: ApiService) { }

  title: string = 'Frontend';
  inputString: string = ``;

  teamInfoSubs: Subscription = Subscription.EMPTY
  teamInformationArr: TeamInfo[] = [];

  onInputChange(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.inputString = event.target.value as string;
  }

  onClick() {
    if (!this.inputString) {
      // can show toast message if no input
      return;
    }
    this.teamInfoSubs = this.apiService
      .addTeamInfo(this.inputString)
      .subscribe(res => {
        this.castToTeamInfo(res);
      },
        console.error
      );
    // show toast message for success
  }

  castToTeamInfo(anyArr: any[]) {
    const teamInfoArr = [];
    for (let i = 0; i < anyArr.length; i++) {
      const teamInfo: TeamInfo = new TeamInfo(anyArr[i][0], anyArr[i][1], anyArr[i][2]);
      teamInfoArr.push(teamInfo);
    }
    this.teamInformationArr = teamInfoArr;
  }

}
