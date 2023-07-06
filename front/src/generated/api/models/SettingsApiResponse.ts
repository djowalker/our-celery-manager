/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface SettingsApiResponse
 */
export interface SettingsApiResponse {
    /**
     * 
     * @type {any}
     * @memberof SettingsApiResponse
     */
    application_name: any | null;
    /**
     * 
     * @type {any}
     * @memberof SettingsApiResponse
     */
    version: any | null;
    /**
     * 
     * @type {any}
     * @memberof SettingsApiResponse
     */
    broker: any | null;
    /**
     * 
     * @type {any}
     * @memberof SettingsApiResponse
     */
    backend: any | null;
}

/**
 * Check if a given object implements the SettingsApiResponse interface.
 */
export function instanceOfSettingsApiResponse(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "application_name" in value;
    isInstance = isInstance && "version" in value;
    isInstance = isInstance && "broker" in value;
    isInstance = isInstance && "backend" in value;

    return isInstance;
}

export function SettingsApiResponseFromJSON(json: any): SettingsApiResponse {
    return SettingsApiResponseFromJSONTyped(json, false);
}

export function SettingsApiResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): SettingsApiResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'application_name': json['application_name'],
        'version': json['version'],
        'broker': json['broker'],
        'backend': json['backend'],
    };
}

export function SettingsApiResponseToJSON(value?: SettingsApiResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'application_name': value.application_name,
        'version': value.version,
        'broker': value.broker,
        'backend': value.backend,
    };
}

