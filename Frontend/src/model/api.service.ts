import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

import {API_URL} from '../../env';

@Injectable()
export class ApiService {
  constructor(private http: HttpClient) {
  }

  addTeamInfo(input: string): Observable<any[]> {
    return this.http.post<any[]>(`${API_URL}/add/teamInfo`, {user_input: input});
  }

  addMatchResult(input: string): Observable<any[]> {
    return this.http.post<any[]>(`${API_URL}/add/matchResult`, {user_input: input});
  }

  getTeamInfo(): Observable<any[]> {
    return this.http.get<any[]>(`${API_URL}/get/teamInfo`);
  }

  getMatchResult(): Observable<any[]> {
    return this.http.get<any[]>(`${API_URL}/get/matchResult`);
  }

  getRanking(): Observable<any[]> {
    return this.http.get<any[]>(`${API_URL}/get/ranking`);
  }

  deleteAll() {
    return this.http.get(`${API_URL}/delete/all`);
  }
}
