import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { API_URL } from '../../env';
import { MatchResult, TeamInfo } from './model';

@Injectable()
export class ApiService {

    constructor(private http: HttpClient) {
    }

    addTeamInfo(input: string): Observable<TeamInfo[]> {
        return this.http.post<TeamInfo[]>(`${API_URL}/add/teamInfo`, { input: input });
    }

    addMatchResult(input: string): Observable<MatchResult> {
        return this.http.post<MatchResult>(`${API_URL}/add/matchResult`, { input: input });
    }

}
